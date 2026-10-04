/**
 * src/features/activities/infrastructure/mappers/activity.mapper.ts
 *
 * Mapeo bidireccional entre los contratos snake_case del backend
 * y las entidades camelCase del frontend.
 */

import type { ActivityDetail, ActivityDetailData, ActivityListItem } from "../../domain/entities/activity.entity";
import type {
  ActivityDetailDataResponse,
  ActivityDetailResponse,
  ActivityListItemResponse,
  ActivityListResponse,
} from "../schemas/activity.schemas";

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
      creatorImage: dto.creator_image ?? undefined,
    };
  },

  toActivityList(dto: ActivityListResponse): ActivityListItem[] {
    return dto.items.map(activityMapper.toActivityListItem);
  },

  toActivityDetail(dto: ActivityDetailResponse | null | undefined): ActivityDetail | null {
    if (!dto) return null;
    return {
      id: dto.id,
      activityId: dto.activity_id,
      latitude: dto.latitude ?? null,
      longitude: dto.longitude ?? null,
      place: dto.place ?? null,
      address: dto.address ?? null,
      description: dto.description ?? null,
    };
  },

  toActivityDetailData(dto: ActivityDetailDataResponse): ActivityDetailData {
    return {
      id: dto.id,
      name: dto.name,
      imageUrl: dto.image_url,
      date: dto.date,
      ownerId: dto.owner_id,
      capacity: dto.capacity,
      status: dto.status,
      creatorName: dto.creator_name ?? undefined,
      creatorImage: dto.creator_image ?? undefined,
      isOwner: dto.is_owner,
      detail: activityMapper.toActivityDetail(dto.detail),
    };
  },
};
