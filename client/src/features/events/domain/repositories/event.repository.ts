/**
 * src/features/events/domain/repositories/event.repository.ts
 *
 * Contrato de repositorio para el módulo de eventos.
 * Sin prefijo 'I' según directrices constitucionales de frontend.
 */

import type {
  ApiActionResult,
  ApiResult,
} from "@/features/shared/domain/types/api-results";
import type { EventListItem, EventScope } from "../entities/event.entity";

export interface EventRepository {
  /**
   * Obtiene la lista de eventos según el ámbito indicado (propios o de terceros).
   */
  listEvents(scope: EventScope): Promise<ApiResult<EventListItem[]>>;

  /**
   * Registra un nuevo evento enviando los datos multipart (imagen, nombre y fecha).
   */
  createEvent(formData: FormData): Promise<ApiActionResult>;
}
