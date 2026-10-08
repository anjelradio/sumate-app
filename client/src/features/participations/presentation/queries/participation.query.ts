import "server-only";
import { cache } from "react";
import type { ParticipatedActivityListItem } from "../../domain/entities/participation.entity";
import { participationRepositoryImpl } from "../../infrastructure/repositories/participation.repository";

export const getMyParticipationsQuery = cache(
  async (): Promise<ParticipatedActivityListItem[]> => {
    const response = await participationRepositoryImpl.listMyParticipations();

    if (!response.ok) {
      throw new Error(
        response.errors?.[0] ?? "Error al cargar el historial de participaciones."
      );
    }

    return response.data;
  }
);
