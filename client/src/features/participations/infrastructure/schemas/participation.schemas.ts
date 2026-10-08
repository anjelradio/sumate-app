/**
 * src/features/participations/infrastructure/schemas/participation.schemas.ts
 *
 * Esquemas Zod para respuestas de API del módulo de participaciones.
 */

import { z } from "zod";

export const ParticipatedActivityItemResponseSchema = z.object({
  id: z.string(),
  name: z.string(),
  image_url: z.string(),
  date: z.string(),
  owner_id: z.string(),
  capacity: z.number().int().positive(),
  status: z.string(),
  enrolled_date: z.string(),
  is_past: z.boolean(),
  creator_name: z.string().nullable().optional(),
  creator_image: z.string().nullable().optional(),
});

export const ParticipatedActivityListResponseSchema = z.object({
  items: z.array(ParticipatedActivityItemResponseSchema),
});

export type ParticipatedActivityItemResponse = z.infer<
  typeof ParticipatedActivityItemResponseSchema
>;
export type ParticipatedActivityListResponse = z.infer<
  typeof ParticipatedActivityListResponseSchema
>;
