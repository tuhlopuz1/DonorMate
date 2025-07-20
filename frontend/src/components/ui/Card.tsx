// src/components/ui/Card.tsx
type CardProps = {
  children: any;
  className?: string;
};

export const Card = ({ children, className = "" }: CardProps) => {
  return (
    <div className={`rounded-2xl border border-gray-200 bg-white p-6 shadow-md ${className}`}>
      {children}
    </div>
  );
};
export default Card