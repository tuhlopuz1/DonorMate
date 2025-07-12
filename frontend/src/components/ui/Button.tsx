// src/components/ui/Button.tsx
import { cn } from "../../shared/lib/utils"; // Опционально: если используешь класс-мерджер

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "outline";
};

export const Button = ({ variant = "primary", className, ...props }: ButtonProps) => {
  const base = "inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-xl transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2";
  
  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
    secondary: "bg-gray-100 text-gray-800 hover:bg-gray-200 focus:ring-gray-300",
    outline: "border border-gray-300 text-gray-800 hover:bg-gray-50 focus:ring-gray-300",
  };

  return (
    <button
      className={cn(base, variants[variant], className)}
      {...props}
    />
  );
};
