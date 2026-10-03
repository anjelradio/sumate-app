/**
 * src/features/activities/domain/repositories/activity.repository.ts
 *
 * Contrato de repositorio para el módulo de actividades.
 * Sin prefijo 'I' según directrices constitucionales de frontend.
 */

import type {
  ApiActionResult,
  ApiResult,
} from "@/features/shared/domain/types/api-results";
import type { ActivityListItem, ActivityScope } from "../entities/activity.entity";

export interface ActivityRepository {
  /**
   * Obtiene la lista de actividades según el ámbito indicado (propias o de terceros).
   */
  listActivities(scope: ActivityScope): Promise<ApiResult<ActivityListItem[]>>;

  /**
   * Registra una nueva actividad enviando los datos multipart (imagen, nombre y fecha).
   */
  createActivity(formData: FormData): Promise<ApiActionResult>;
}
