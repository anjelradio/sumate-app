import "server-only";
import { cache } from "react";
import type { EventListItem, EventScope } from "../../domain/entities/event.entity";
import { eventRepositoryImpl } from "../../infrastructure/repositories/event.repository";

export const getEventsQuery = cache(async (scope: EventScope): Promise<EventListItem[]> => {
  const response = await eventRepositoryImpl.listEvents(scope);

  if (!response.ok) {
    throw new Error(response.errors?.[0] ?? "Error al cargar los eventos.");
  }

  return response.data;
});
