/**
 * src/features/events/infrastructure/repositories/event.repository.ts
 *
 * Implementación HTTP de EventRepository utilizando api-client.
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
  EventListItem,
  EventScope,
} from "../../domain/entities/event.entity";
import type { EventRepository } from "../../domain/repositories/event.repository";
import { eventMapper } from "../mappers/event.mapper";
import { EventListResponseSchema } from "../schemas/event.schemas";

const BASE_URL = `${process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000/api"}/events`;

export const eventRepositoryImpl: EventRepository = {
  async listEvents(scope: EventScope): Promise<ApiResult<EventListItem[]>> {
    const url = new URL(BASE_URL);
    url.searchParams.set("scope", scope);

    return apiRequestData({
      url: url.toString(),
      method: "GET",
      responseSchema: EventListResponseSchema,
      mapData: eventMapper.toEventList,
      fallbackMessage: "Error al cargar la lista de eventos.",
    });
  },

  async createEvent(formData: FormData): Promise<ApiActionResult> {
    return apiRequestFormStatus({
      url: BASE_URL,
      method: "POST",
      body: formData,
      fallbackMessage: "Error al registrar el evento.",
    });
  },
};
