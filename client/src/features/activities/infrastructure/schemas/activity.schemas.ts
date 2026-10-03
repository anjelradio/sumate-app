/**
 * src/features/activities/infrastructure/schemas/activity.schemas.ts
 *
 * Esquemas Zod para validación de respuestas de API y formularios de actividades.
 */

import { z } from "zod";

export const ActivityListItemResponseSchema = z.object({
  id: z.string(),
  name: z.string(),
  image_url: z.string(),
  date: z.string(),
  owner_id: z.string(),
  capacity: z.number().int().positive(),
  status: z.enum(["draft", "active", "closed"]),
  creator_name: z.string().nullable().optional(),
});

export const ActivityListResponseSchema = z.object({
  items: z.array(ActivityListItemResponseSchema),
});

export type ActivityListItemResponse = z.infer<typeof ActivityListItemResponseSchema>;
export type ActivityListResponse = z.infer<typeof ActivityListResponseSchema>;

/**
 * Esquema de validación del formulario de creación de actividades.
 */
export const CreateActivityFormSchema = z.object({
  name: z
    .string({ message: "El nombre de la actividad es obligatorio." })
    .min(3, "El nombre debe tener al menos 3 caracteres.")
    .max(120, "El nombre no puede superar los 120 caracteres."),
  date: z
    .string({ message: "La fecha de la actividad es obligatoria." })
    .min(1, "Por favor selecciona una fecha y hora."),
  capacity: z
    .number({ message: "La cantidad de plazas debe ser un número entero." })
    .int("La cantidad de plazas debe ser un número entero.")
    .positive("La cantidad de plazas debe ser mayor a cero.")
    .max(10000, "La cantidad de plazas no puede superar 10,000."),
  image: z
    .custom<File>(
      (val) => typeof window !== "undefined" && val instanceof File && val.size > 0,
      { message: "Debes seleccionar una imagen para la actividad." }
    ),
});

export type CreateActivityFormData = z.infer<typeof CreateActivityFormSchema>;
