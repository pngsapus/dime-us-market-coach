import Link from "next/link";

export function ErrorState({
  title = "ไม่สามารถเชื่อมต่อข้อมูลจำลองจาก backend ได้",
  detail = "กรุณาตรวจสอบว่า backend mock API ทำงานอยู่ แล้วลองโหลดหน้านี้อีกครั้ง",
  retryHref = ".",
}: {
  title?: string;
  detail?: string;
  retryHref?: string;
}) {
  return (
    <section className="rounded-md border border-red-100 bg-red-50 p-5 text-sm">
      <h2 className="text-base font-semibold text-danger">{title}</h2>
      <p className="mt-2 leading-6 text-red-900">{detail}</p>
      <div className="mt-4 flex flex-wrap gap-2">
        <Link href={retryHref} className="rounded-md bg-white px-3 py-2 text-sm font-medium text-danger shadow-sm">
          ลองใหม่
        </Link>
        <Link href="/data-status" className="rounded-md border border-red-200 px-3 py-2 text-sm font-medium text-danger">
          ตรวจสอบสถานะข้อมูล
        </Link>
      </div>
    </section>
  );
}
