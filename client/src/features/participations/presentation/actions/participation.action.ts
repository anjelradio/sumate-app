"use server";

import { revalidatePath, updateTag } from "next/cache";
import type { ApiActionResult } from "@/features/shared/domain/types/api-results";
import { errorResult } from "@/features/shared/infrastructure/errors/api-error";
import { participationRepositoryImpl } from "../../infrastructure/repositories/participation.repository";

export async function joinActivityAction(activityId: string): Promise<ApiActionResult> {
  if (!activityId || !activityId.trim()) {
    return errorResult("ID de actividad inválido.");
  }

  const result = await participationRepositoryImpl.joinActivity(activityId);

  if (result.ok) {
    revalidatePath(`/activities/${activityId}`);
    revalidatePath("/explore");
    revalidatePath("/recently");
    updateTag("activities");
    updateTag(`activity-${activityId}`);
    updateTag("participations");
    updateTag("participations-me");
  }

  return result;
}

export async function leaveActivityAction(activityId: string): Promise<ApiActionResult> {
  if (!activityId || !activityId.trim()) {
    return errorResult("ID de actividad inválido.");
  }

  const result = await participationRepositoryImpl.leaveActivity(activityId);

  if (result.ok) {
    revalidatePath(`/activities/${activityId}`);
    revalidatePath("/explore");
    revalidatePath("/recently");
    updateTag("activities");
    updateTag(`activity-${activityId}`);
    updateTag("participations");
    updateTag("participations-me");
  }

  return result;
}
