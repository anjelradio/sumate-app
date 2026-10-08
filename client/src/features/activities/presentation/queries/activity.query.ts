import "server-only";
import { cache } from "react";
import type {
  ActivityDetailData,
  ActivityListItem,
  MyActivityListItem,
} from "../../domain/entities/activity.entity";
import { activityRepositoryImpl } from "../../infrastructure/repositories/activity.repository";

export const getExploreActivitiesQuery = cache(async (): Promise<ActivityListItem[]> => {
  const response = await activityRepositoryImpl.listExplore();

  if (!response.ok) {
    throw new Error(response.errors?.[0] ?? "Error al cargar las actividades para explorar.");
  }

  return response.data;
});

export const getMyActivitiesQuery = cache(async (): Promise<MyActivityListItem[]> => {
  const response = await activityRepositoryImpl.listMyActivities();

  if (!response.ok) {
    throw new Error(response.errors?.[0] ?? "Error al cargar mis actividades.");
  }

  return response.data;
});

export const getActivityDetailQuery = cache(
  async (id: string): Promise<ActivityDetailData | null> => {
    const response = await activityRepositoryImpl.getActivityDetail(id);

    if (!response.ok) {
      if (response.statusCode === 404) {
        return null;
      }
      throw new Error(response.errors?.[0] ?? "Error al cargar los detalles de la actividad.");
    }

    return response.data;
  }
);

