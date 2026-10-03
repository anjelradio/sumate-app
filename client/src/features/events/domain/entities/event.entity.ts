/**
 * src/features/events/domain/entities/event.entity.ts
 *
 * Entidades y tipos de dominio para el módulo de eventos.
 * TypeScript puro sin dependencias de infraestructura ni frameworks.
 */

export type Event = {
  id: string;
  name: string;
  ownerId: string;
  imageUrl: string;
  date: string; // Formato ISO 8601 string
  creatorName?: string;
};

export type EventListItem = Pick<
  Event,
  "id" | "name" | "imageUrl" | "date" | "ownerId" | "creatorName"
>;

export type EventScope = "mine" | "others";
