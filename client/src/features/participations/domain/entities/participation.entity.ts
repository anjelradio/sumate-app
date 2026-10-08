/**
 * src/features/participations/domain/entities/participation.entity.ts
 *
 * Entidades y tipos de dominio para el módulo de participaciones.
 */

export type Participation = {
  id: string;
  activityId: string;
  userId: string;
  createdAt: string;
};

export type ParticipatedActivityListItem = {
  id: string;
  name: string;
  imageUrl: string;
  date: string;
  ownerId: string;
  capacity: number;
  status: string;
  enrolledDate: string;
  isPast: boolean;
  creatorName?: string;
  creatorImage?: string;
};

export type ParticipationFilter = "all" | "upcoming" | "past";
