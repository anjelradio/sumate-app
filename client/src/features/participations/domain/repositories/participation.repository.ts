/**
 * src/features/participations/domain/repositories/participation.repository.ts
 *
 * Contrato de repositorio para el módulo de participaciones.
 */

import type {
  ApiActionResult,
  ApiResult,
} from "@/features/shared/domain/types/api-results";
import type { ParticipatedActivityListItem } from "../entities/participation.entity";

export interface ParticipationRepository {
  /**
   * Registra la participación del usuario actual en una actividad.
   */
  joinActivity(activityId: string): Promise<ApiActionResult>;

  /**
   * Cancela la participación del usuario actual en una actividad.
   */
  leaveActivity(activityId: string): Promise<ApiActionResult>;

  /**
   * Lista las actividades en las que participa o ha participado el usuario actual.
   */
  listMyParticipations(): Promise<ApiResult<ParticipatedActivityListItem[]>>;
}
