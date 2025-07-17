import React, { useEffect, useRef, useState } from "react";
import { BrowserQRCodeReader } from "@zxing/browser";
import type { IScannerControls } from "@zxing/browser";

const QrScanner: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [result, setResult] = useState<string | null>(null);
  const [isFrontCamera, setIsFrontCamera] = useState(false);
  const controlsRef = useRef<IScannerControls | null>(null);

  useEffect(() => {
    const codeReader = new BrowserQRCodeReader();

    const startScanner = async () => {
      try {
        // Пытаемся запустить заднюю камеру (environment)
        const controls = await codeReader.decodeFromConstraints(
          {
            video: {
              facingMode: { exact: "environment" },
              width: { ideal: 1280 },
              height: { ideal: 720 },
            },
          },
          videoRef.current!,
          (result, error) => {
            console.log(error)
            if (result) {
              setResult(result.getText());
              controlsRef.current?.stop();
            }
          }
        );
        controlsRef.current = controls;
        setIsFrontCamera(false);
      } catch (environmentError) {
        console.log("Задняя камера недоступна, пробуем переднюю...", environmentError);
        try {
          // Если задняя камера недоступна, пробуем переднюю (user)
          const controls = await codeReader.decodeFromConstraints(
            {
              video: {
                facingMode: { exact: "user" },
                width: { ideal: 1280 },
                height: { ideal: 720 },
              },
            },
            videoRef.current!,
            (result, error) => {
                console.log(error)
              if (result) {
                setResult(result.getText());
                controlsRef.current?.stop();
              }
            }
          );
          controlsRef.current = controls;
          setIsFrontCamera(true);
        } catch (userError) {
          console.error("Ошибка при инициализации камеры:", userError);
        }
      }
    };

    startScanner();

    return () => {
      controlsRef.current?.stop();
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black">

      {result ? (
        <div className="bg-green-100 text-green-800 p-4 rounded-xl shadow-md max-w-sm text-center">
          <p className="mb-2 font-semibold">✅ QR-код:</p>
          <p className="break-words">{result}</p>
        </div>
      ) : (
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

          {/* Квадратная рамка по центру */}
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="border-4 border-dashed border-white rounded-lg" 
              style={{ width: "90%", aspectRatio: "1 / 1" }}
            />
          </div>  
        </div>

      )}
    </div>
  );
};

export default QrScanner;