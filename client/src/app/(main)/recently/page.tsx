import { Clock } from "lucide-react";

export default function RecentlyPage() {
  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
      <div className="w-16 h-16 rounded-full bg-slate-100 text-zinc-600 flex items-center justify-center mb-3">
        <Clock className="w-8 h-8" />
      </div>
      <h3 className="text-lg font-bold text-zinc-800">
        Actividades recientes
      </h3>
      <p className="text-sm text-zinc-500 mt-1 max-w-xs leading-relaxed">
        Aquí verás las actividades más recientes y tu historial de interacción en la comunidad.
      </p>
    </div>
  );
}
