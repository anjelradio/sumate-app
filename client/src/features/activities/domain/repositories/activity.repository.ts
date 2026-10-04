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
import type {
  ActivityDetailData,
  ActivityListItem,
  ActivityScope,
} from "../entities/activity.entity";

export interface ActivityRepository {
  /**
   * Obtiene la lista de actividades según el ámbito indicado (propias o de terceros).
   */
  listActivities(scope: ActivityScope): Promise<ApiResult<ActivityListItem[]>>;

  /**
   * Obtiene el detalle completo de una actividad por su ID.
   */
  getActivityDetail(id: string): Promise<ApiResult<ActivityDetailData>>;

  /**
   * Registra una nueva actividad enviando los datos multipart (imagen, nombre y fecha).
   */
  createActivity(formData: FormData): Promise<ApiActionResult>;

  /**
   * Actualiza la ubicación geográfica y resuelve el lugar y dirección mediante Nominatim.
   */
  updateLocation(
    id: string,
    data: { latitude: number; longitude: number }
  ): Promise<ApiActionResult>;

  /**
   * Actualiza la descripción de la actividad.
   */
  updateDescription(
    id: string,
    data: { description: string }
  ): Promise<ApiActionResult>;

  /**
   * Reemplaza la imagen de portada de la actividad.
   */
  updateImage(id: string, formData: FormData): Promise<ApiActionResult>;

  /**
   * Actualiza los datos base (título, fecha y cupos) de la actividad.
   */
  updateInfo(
    id: string,
    data: { name?: string; date?: string; capacity?: number }
  ): Promise<ApiActionResult>;

  /**
   * Publica la actividad cambiando su estado a active tras validar completitud.
   */
  publishActivity(id: string): Promise<ApiActionResult>;

  /**
   * Cierra la convocatoria de la actividad.
   */
  closeActivity(id: string): Promise<ApiActionResult>;
}

