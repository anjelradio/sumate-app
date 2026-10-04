/**
 * src/features/activities/infrastructure/repositories/activity.repository.ts
 *
 * Implementación HTTP de ActivityRepository utilizando api-client.
 */

import type {
  ApiActionResult,
  ApiResult,
} from "@/features/shared/domain/types/api-results";
import {
  apiRequestData,
  apiRequestFormStatus,
  apiRequestStatus,
} from "@/features/shared/infrastructure/http/api-client";
import type {
  ActivityDetailData,
  ActivityListItem,
  ActivityScope,
} from "../../domain/entities/activity.entity";
import type { ActivityRepository } from "../../domain/repositories/activity.repository";
import { activityMapper } from "../mappers/activity.mapper";
import {
  ActivityDetailDataResponseSchema,
  ActivityListResponseSchema,
} from "../schemas/activity.schemas";

const BASE_URL = `${process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000/api"}/activities`;

export const activityRepositoryImpl: ActivityRepository = {
  async listActivities(scope: ActivityScope): Promise<ApiResult<ActivityListItem[]>> {
    const url = new URL(BASE_URL);
    url.searchParams.set("scope", scope);

    return apiRequestData({
      url: url.toString(),
      method: "GET",
      next: { revalidate: 30, tags: ["activities", `activities-${scope}`] },
      responseSchema: ActivityListResponseSchema,
      mapData: activityMapper.toActivityList,
      fallbackMessage: "Error al cargar la lista de actividades.",
    });
  },

  async getActivityDetail(id: string): Promise<ApiResult<ActivityDetailData>> {
    return apiRequestData({
      url: `${BASE_URL}/${id}`,
      method: "GET",
      next: { revalidate: 0, tags: ["activities", `activity-${id}`] },
      responseSchema: ActivityDetailDataResponseSchema,
      mapData: activityMapper.toActivityDetailData,
      fallbackMessage: "Error al cargar el detalle de la actividad.",
    });
  },

  async createActivity(formData: FormData): Promise<ApiActionResult> {
    return apiRequestFormStatus({
      url: BASE_URL,
      method: "POST",
      body: formData,
      fallbackMessage: "Error al registrar la actividad.",
    });
  },

  async updateLocation(
    id: string,
    data: { latitude: number; longitude: number; place?: string }
  ): Promise<ApiActionResult> {
    return apiRequestStatus({
      url: `${BASE_URL}/${id}/location`,
      method: "PATCH",
      body: data,
      fallbackMessage: "Error al actualizar la ubicación.",
    });
  },

  async updateDescription(
    id: string,
    data: { description: string }
  ): Promise<ApiActionResult> {
    return apiRequestStatus({
      url: `${BASE_URL}/${id}/description`,
      method: "PATCH",
      body: data,
      fallbackMessage: "Error al actualizar la descripción.",
    });
  },

  async updateImage(id: string, formData: FormData): Promise<ApiActionResult> {
    return apiRequestFormStatus({
      url: `${BASE_URL}/${id}/image`,
      method: "PATCH",
      body: formData,
      fallbackMessage: "Error al actualizar la foto de portada.",
    });
  },

  async updateInfo(
    id: string,
    data: { name?: string; date?: string; capacity?: number }
  ): Promise<ApiActionResult> {
    return apiRequestStatus({
      url: `${BASE_URL}/${id}/info`,
      method: "PATCH",
      body: data,
      fallbackMessage: "Error al actualizar los datos base de la actividad.",
    });
  },

  async publishActivity(id: string): Promise<ApiActionResult> {
    return apiRequestStatus({
      url: `${BASE_URL}/${id}/publish`,
      method: "POST",
      fallbackMessage: "Error al publicar la actividad.",
    });
  },

  async closeActivity(id: string): Promise<ApiActionResult> {
    return apiRequestStatus({
      url: `${BASE_URL}/${id}/close`,
      method: "POST",
      fallbackMessage: "Error al cerrar la convocatoria de la actividad.",
    });
  },
};

