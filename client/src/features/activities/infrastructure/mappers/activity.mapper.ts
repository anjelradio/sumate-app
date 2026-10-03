/**
 * src/features/activities/infrastructure/mappers/activity.mapper.ts
 *
 * Mapeo bidireccional entre los contratos snake_case del backend
 * y las entidades camelCase del frontend.
 */

import type { ActivityListItem } from "../../domain/entities/activity.entity";
import type { ActivityListItemResponse, ActivityListResponse } from "../schemas/activity.schemas";

export const activityMapper = {
  toActivityListItem(dto: ActivityListItemResponse): ActivityListItem {
    return {
      id: dto.id,
      name: dto.name,
      imageUrl: dto.image_url,
      date: dto.date,
      ownerId: dto.owner_id,
      capacity: dto.capacity,
      status: dto.status,
      creatorName: dto.creator_name ?? undefined,
    };
  },

  toActivityList(dto: ActivityListResponse): ActivityListItem[] {
    return dto.items.map(activityMapper.toActivityListItem);
  },
};
