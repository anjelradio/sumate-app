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
} from "@/features/shared/infrastructure/http/api-client";
import type {
  ActivityListItem,
  ActivityScope,
} from "../../domain/entities/activity.entity";
import type { ActivityRepository } from "../../domain/repositories/activity.repository";
import { activityMapper } from "../mappers/activity.mapper";
import { ActivityListResponseSchema } from "../schemas/activity.schemas";

const BASE_URL = `${process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000/api"}/activities`;

export const activityRepositoryImpl: ActivityRepository = {
  async listActivities(scope: ActivityScope): Promise<ApiResult<ActivityListItem[]>> {
    const url = new URL(BASE_URL);
    url.searchParams.set("scope", scope);

    return apiRequestData({
      url: url.toString(),
      method: "GET",
      responseSchema: ActivityListResponseSchema,
      mapData: activityMapper.toActivityList,
      fallbackMessage: "Error al cargar la lista de actividades.",
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
};
