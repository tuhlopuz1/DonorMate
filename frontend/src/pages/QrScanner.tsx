import React, { useEffect, useRef, useState } from "react";
import { BrowserQRCodeReader } from "@zxing/browser";
import type { IScannerControls } from "@zxing/browser";


const ZxingQrScanner: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [result, setResult] = useState<string | null>(null);
  const controlsRef = useRef<IScannerControls | null>(null);

  useEffect(() => {
    const codeReader = new BrowserQRCodeReader();

    BrowserQRCodeReader.listVideoInputDevices()
      .then((devices) => {
        if (devices.length === 0) {
          throw new Error("Камера не найдена");
        }

        const deviceId = devices[0].deviceId;

        codeReader.decodeFromVideoDevice(
          deviceId,
          videoRef.current!,
          (result, error, controls) => {
            console.log(error)
            if (controls && !controlsRef.current) {
              controlsRef.current = controls;
            }

            if (result) {
              setResult(result.getText());
              controls?.stop(); // Останавливаем сканер
            }
          }
        );
      })
      .catch((err) => {
        console.error("Ошибка при инициализации камеры:", err);
      });

    return () => {
      controlsRef.current?.stop(); // Остановка при размонтировании
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Сканер QR-кодов (ZXing)</h1>

      {result ? (
        <div className="bg-green-100 text-green-800 p-4 rounded-xl shadow-md max-w-sm text-center">
          <p className="mb-2 font-semibold">✅ QR-код:</p>
          <p className="break-words">{result}</p>
        </div>
      ) : (
        <video
          ref={videoRef}
          className="w-full max-w-md rounded-md shadow-lg"
          autoPlay
          muted
        />
      )}
    </div>
  );
};

export default ZxingQrScanner;
