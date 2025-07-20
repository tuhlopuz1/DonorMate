import React, { useEffect, useRef, useState } from "react";
import { BrowserQRCodeReader } from "@zxing/browser";
import type { IScannerControls } from "@zxing/browser";
import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

const MySwal = withReactContent(Swal);

const QrScanner: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isFrontCamera, setIsFrontCamera] = useState(false);
  const controlsRef = useRef<IScannerControls | null>(null);
  const codeReaderRef = useRef(new BrowserQRCodeReader());

  const checkQr = async (token: string) => {
    const res = await fetch("/api/check-qr", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      throw new Error("Ошибка при верификации токена");
    }

    return await res.json();
  };

  const acceptDonation = async (token: string) => {
    const res = await fetch("/api/accept-donation", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      throw new Error("Ошибка при подтверждении посещения");
    }
  };

  const handleResult = async (result: any, error: any) => {
    if (error) {
      console.log(error);
    }
    if (result) {
      const token = result.getText();
      controlsRef.current?.stop(); // Останавливаем сканер

      try {
        const userData = await checkQr(token);
        await showUserInfoAlert(userData, token);
      } catch (e) {
        console.error(e);
        await Swal.fire("Ошибка", "Неверный QR-код или ошибка сервера", "error");
        startScanner(); // Перезапустить сканер
      }
    }
  };

  const startScanner = async () => {
    const codeReader = codeReaderRef.current;
    try {
      const controls = await codeReader.decodeFromConstraints(
        {
          video: {
            facingMode: { exact: "environment" },
            width: { ideal: 1280 },
            height: { ideal: 720 },
          },
        },
        videoRef.current!,
        handleResult
      );
      controlsRef.current = controls;
      setIsFrontCamera(false);
    } catch (environmentError) {
      console.log("Задняя камера недоступна, пробуем переднюю...", environmentError);
      try {
        const controls = await codeReader.decodeFromConstraints(
          {
            video: {
              facingMode: { exact: "user" },
              width: { ideal: 1280 },
              height: { ideal: 720 },
            },
          },
          videoRef.current!,
          handleResult
        );
        controlsRef.current = controls;
        setIsFrontCamera(true);
      } catch (userError) {
        console.error("Ошибка при инициализации камеры:", userError);
      }
    }
  };

  const showUserInfoAlert = async (
    userData: {
      phone: number;
      fsp: string;
    },
    token: string
  ) => {
    const result = await MySwal.fire({
      title: "Данные пользователя",
      html: `<p><strong>Телефон:</strong> ${userData.phone}</p>
             <p><strong>ФСП:</strong> ${userData.fsp}</p>`,
      showCancelButton: true,
      confirmButtonText: "Отметить как пришедшего",
      cancelButtonText: "Отмена",
    });

    if (result.isConfirmed) {
      try {
        await acceptDonation(token);
        await Swal.fire("Успешно", "Посещение подтверждено", "success");
      } catch (err) {
        await Swal.fire("Ошибка", "Не удалось подтвердить посещение", "error");
      }
    }

    // Перезапуск сканера после действия
    startScanner();
  };

  useEffect(() => {
    startScanner();

    return () => {
      controlsRef.current?.stop();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black">
      <div className="relative w-full max-w-md">
        <video
          ref={videoRef}
          className="w-full h-auto rounded-md shadow-lg"
          style={{
            transform: isFrontCamera ? "scaleX(-1)" : "none",
          }}
          autoPlay
          muted
        />
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div
            className="border-4 border-dashed border-white rounded-lg"
            style={{ width: "90%", aspectRatio: "1 / 1" }}
          />
        </div>
      </div>
    </div>
  );
};

export default QrScanner;
