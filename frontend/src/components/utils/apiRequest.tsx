let isRefreshing = false;
let refreshPromise: Promise<string> | null = null;

function getAccessToken(): string | null {
    const token = localStorage.getItem('access_token');
    if (!token) {
        localStorage.setItem('location_after_login', window.location.href);
    }
    return token;
}

function getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
}

async function refreshToken(): Promise<string> {
    const response = await fetch('https://api.donor.vickz.ru/api/v2/refresh', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getRefreshToken()}`
        },
    });

    if (!response.ok) {
        throw new Error('Failed to refresh token');
    }

    const data: { new_access_token: string } = await response.json();
    localStorage.setItem('access_token', data.new_access_token);
    return data.new_access_token;
}

interface ApiRequestOptions {
    url: string;
    method?: string;
    params?: Record<string, string | number>;
    body?: Record<string, any> | null;
    auth?: boolean;
    retry?: boolean;
    headers?: Record<string, string>;
}

async function apiRequest({
    url,
    method = 'GET',
    params = {},
    body = null,
    auth = false,
    retry = true,
    headers = {
        'Content-Type': 'application/json',
    }
}: ApiRequestOptions): Promise<Response> {
    const queryString = new URLSearchParams(params as Record<string, string>).toString();
    const fullUrl = queryString ? `${url}?${queryString}` : url;

    const finalHeaders = { ...headers };

    if (auth) {
        finalHeaders['Authorization'] = `Bearer ${getAccessToken()}`;
    }

    const options: RequestInit = {
        method,
        headers: finalHeaders,
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    let response = await fetch(fullUrl, options);

    if (response.status === 401 && auth && retry) {
        try {
            if (!isRefreshing) {
                isRefreshing = true;
                refreshPromise = refreshToken();
            }

            const newAccessToken = await refreshPromise;
            isRefreshing = false;

            finalHeaders['Authorization'] = `Bearer ${newAccessToken}`;

            const retryOptions: RequestInit = {
                ...options,
                headers: finalHeaders
            };

            response = await fetch(fullUrl, retryOptions);
        } catch (error) {
            localStorage.removeItem('access_token');

            if (!window.location.href.endsWith('login')) {
                localStorage.setItem('location_after_login', window.location.href);
            }
            window.location.href = '/#/login';
            throw error;
        }
    }

    return response;
}

export default apiRequest;
