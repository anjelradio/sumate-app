/**
 * src/features/activities/domain/entities/activity.entity.ts
 *
 * Entidades y tipos de dominio para el módulo de actividades.
 * TypeScript puro sin dependencias de infraestructura ni frameworks.
 */

export type ActivityStatus = "draft" | "active" | "closed";

export type Activity = {
  id: string;
  name: string;
  ownerId: string;
  imageUrl: string;
  date: string; // Formato ISO 8601 string
  capacity: number;
  status: ActivityStatus;
  creatorName?: string;
  creatorImage?: string;
};

export type ActivityListItem = Pick<
  Activity,
  | "id"
  | "name"
  | "imageUrl"
  | "date"
  | "ownerId"
  | "capacity"
  | "status"
  | "creatorName"
  | "creatorImage"
>;

export type ActivityDetail = {
  id: string;
  activityId: string;
  latitude: number | null;
  longitude: number | null;
  place: string | null;
  address: string | null;
  description: string | null;
};

export type ActivityDetailData = Activity & {
  isOwner: boolean;
  detail: ActivityDetail | null;
};

export type ActivityScope = "mine" | "others";
