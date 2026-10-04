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
  creator_image: z.string().nullable().optional(),
});

export const ActivityListResponseSchema = z.object({
  items: z.array(ActivityListItemResponseSchema),
});

export const ActivityDetailResponseSchema = z.object({
  id: z.string(),
  activity_id: z.string(),
  latitude: z.number().nullable().optional(),
  longitude: z.number().nullable().optional(),
  place: z.string().nullable().optional(),
  address: z.string().nullable().optional(),
  description: z.string().nullable().optional(),
});

export const ActivityDetailDataResponseSchema = z.object({
  id: z.string(),
  name: z.string(),
  image_url: z.string(),
  date: z.string(),
  owner_id: z.string(),
  capacity: z.number().int().positive(),
  status: z.enum(["draft", "active", "closed"]),
  creator_name: z.string().nullable().optional(),
  creator_image: z.string().nullable().optional(),
  is_owner: z.boolean(),
  detail: ActivityDetailResponseSchema.nullable().optional(),
});

export type ActivityListItemResponse = z.infer<typeof ActivityListItemResponseSchema>;
export type ActivityListResponse = z.infer<typeof ActivityListResponseSchema>;
export type ActivityDetailResponse = z.infer<typeof ActivityDetailResponseSchema>;
export type ActivityDetailDataResponse = z.infer<typeof ActivityDetailDataResponseSchema>;

export const UpdateLocationSchema = z.object({
  latitude: z.number().min(-90).max(90),
  longitude: z.number().min(-180).max(180),
});

export const UpdateDescriptionSchema = z.object({
  description: z.string().min(1, "La descripción no puede estar vacía.").max(5000),
});

export const UpdateActivityInfoSchema = z.object({
  name: z.string().min(3).max(120).optional(),
  date: z.string().min(1).optional(),
  capacity: z.number().int().positive().max(10000).optional(),
});

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

export const EditTitleSchema = z.object({
  name: z
    .string({ message: "El título es obligatorio." })
    .trim()
    .min(3, "El título debe tener al menos 3 caracteres.")
    .max(120, "El título no puede superar los 120 caracteres."),
});
export type EditTitleFormData = z.infer<typeof EditTitleSchema>;

export const EditDateSchema = z.object({
  date: z
    .string({ message: "La fecha es obligatoria." })
    .min(1, "Por favor selecciona una fecha y hora."),
});
export type EditDateFormData = z.infer<typeof EditDateSchema>;

export const EditCapacitySchema = z.object({
  capacity: z
    .number({ message: "Los cupos deben ser un número." })
    .int("Los cupos deben ser un número entero.")
    .positive("Debe haber al menos 1 cupo disponible.")
    .max(10000, "Los cupos no pueden superar 10,000."),
});
export type EditCapacityFormData = z.infer<typeof EditCapacitySchema>;

export const EditDescriptionSchema = z.object({
  description: z
    .string({ message: "La descripción es requerida." })
    .trim()
    .min(10, "La descripción debe tener al menos 10 caracteres.")
    .max(5000, "La descripción no puede superar los 5,000 caracteres."),
});
export type EditDescriptionFormData = z.infer<typeof EditDescriptionSchema>;
