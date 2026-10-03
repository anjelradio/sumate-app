/**
 * src/features/events/infrastructure/schemas/event.schemas.ts
 *
 * Esquemas Zod para validación de respuestas de API y formularios de eventos.
 */

import { z } from "zod";

export const EventListItemResponseSchema = z.object({
  id: z.string(),
  name: z.string(),
  image_url: z.string(),
  date: z.string(),
  owner_id: z.string(),
  creator_name: z.string().nullable().optional(),
});

export const EventListResponseSchema = z.object({
  items: z.array(EventListItemResponseSchema),
});

export type EventListItemResponse = z.infer<typeof EventListItemResponseSchema>;
export type EventListResponse = z.infer<typeof EventListResponseSchema>;

/**
 * Esquema de validación del formulario de creación de eventos.
 */
export const CreateEventFormSchema = z.object({
  name: z
    .string({ message: "El nombre del evento es obligatorio." })
    .min(3, "El nombre debe tener al menos 3 caracteres.")
    .max(120, "El nombre no puede superar los 120 caracteres."),
  date: z
    .string({ message: "La fecha del evento es obligatoria." })
    .min(1, "Por favor selecciona una fecha y hora."),
  image: z
    .custom<File>(
      (val) => typeof window !== "undefined" && val instanceof File && val.size > 0,
      { message: "Debes seleccionar una imagen para el evento." }
    ),
});

export type CreateEventFormData = z.infer<typeof CreateEventFormSchema>;
