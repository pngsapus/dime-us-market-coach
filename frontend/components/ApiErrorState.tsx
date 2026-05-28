import { ErrorState } from "./ErrorState";

export function ApiErrorState({ title = "ไม่สามารถเชื่อมต่อข้อมูลจำลองจาก backend ได้", detail, retryHref }: { title?: string; detail?: string; retryHref?: string }) {
  return <ErrorState title={title} detail={detail} retryHref={retryHref ?? "."} />;
}
