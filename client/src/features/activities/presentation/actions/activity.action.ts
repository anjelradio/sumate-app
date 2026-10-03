"use server";

import { revalidatePath, updateTag } from "next/cache";
import type { ApiActionResult } from "@/features/shared/domain/types/api-results";
import { errorResult } from "@/features/shared/infrastructure/errors/api-error";
import { activityRepositoryImpl } from "../../infrastructure/repositories/activity.repository";

export async function createActivityAction(formData: FormData): Promise<ApiActionResult> {
  const name = formData.get("name");
  const date = formData.get("date");
  const capacityRaw = formData.get("capacity");
  const image = formData.get("image");

  if (!name || typeof name !== "string" || !name.trim()) {
    return errorResult("El nombre de la actividad es requerido.");
  }

  if (!date || typeof date !== "string" || !date.trim()) {
    return errorResult("La fecha de la actividad es obligatoria.");
  }

  const capacity = Number(capacityRaw);
  if (!capacityRaw || isNaN(capacity) || !Number.isInteger(capacity) || capacity <= 0) {
    return errorResult("La cantidad de plazas debe ser un número entero mayor a cero.");
  }

  if (capacity > 10000) {
    return errorResult("La cantidad de plazas no puede superar 10,000.");
  }

  if (!image || !(image instanceof File) || image.size === 0) {
    return errorResult("Debes seleccionar una imagen para la actividad.");
  }

  const result = await activityRepositoryImpl.createActivity(formData);

  if (result.ok) {
    revalidatePath("/my-activities");
    revalidatePath("/explore");
    updateTag("activities");
  }

  return result;
}
