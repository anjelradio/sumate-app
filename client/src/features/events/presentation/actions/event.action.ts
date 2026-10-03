"use server";

import { revalidatePath } from "next/cache";
import type { ApiActionResult } from "@/features/shared/domain/types/api-results";
import { errorResult } from "@/features/shared/infrastructure/errors/api-error";
import { eventRepositoryImpl } from "../../infrastructure/repositories/event.repository";

export async function createEventAction(formData: FormData): Promise<ApiActionResult> {
  const name = formData.get("name");
  const date = formData.get("date");
  const image = formData.get("image");

  if (!name || typeof name !== "string" || !name.trim()) {
    return errorResult("El nombre del evento es requerido.");
  }

  if (!date || typeof date !== "string" || !date.trim()) {
    return errorResult("La fecha del evento es obligatoria.");
  }

  if (!image || !(image instanceof File) || image.size === 0) {
    return errorResult("Debes seleccionar una imagen para el evento.");
  }

  const result = await eventRepositoryImpl.createEvent(formData);

  if (result.ok) {
    revalidatePath("/home");
  }

  return result;
}
