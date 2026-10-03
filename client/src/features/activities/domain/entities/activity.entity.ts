/**
 * src/features/activities/domain/entities/activity.entity.ts
 *
 * Entidades y tipos de dominio para el módulo de actividades.
 * TypeScript puro sin dependencias de infraestructura ni frameworks.
 */

export type Activity = {
  id: string;
  name: string;
  ownerId: string;
  imageUrl: string;
  date: string; // Formato ISO 8601 string
  creatorName?: string;
};

export type ActivityListItem = Pick<
  Activity,
  "id" | "name" | "imageUrl" | "date" | "ownerId" | "creatorName"
>;

export type ActivityScope = "mine" | "others";
