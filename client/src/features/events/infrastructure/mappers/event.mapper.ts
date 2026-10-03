/**
 * src/features/events/infrastructure/mappers/event.mapper.ts
 *
 * Mapeo bidireccional entre los contratos snake_case del backend
 * y las entidades camelCase del frontend.
 */

import type { EventListItem } from "../../domain/entities/event.entity";
import type { EventListItemResponse, EventListResponse } from "../schemas/event.schemas";

export const eventMapper = {
  toEventListItem(dto: EventListItemResponse): EventListItem {
    return {
      id: dto.id,
      name: dto.name,
      imageUrl: dto.image_url,
      date: dto.date,
      ownerId: dto.owner_id,
      creatorName: dto.creator_name ?? undefined,
    };
  },

  toEventList(dto: EventListResponse): EventListItem[] {
    return dto.items.map(eventMapper.toEventListItem);
  },
};
