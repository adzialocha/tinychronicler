import { DateTime } from 'luxon';

export function formatDate(iso: string) {
  const formatted = DateTime.fromISO(iso, {
    zone: 'utc',
  })
    .setZone('system')
    .toFormat('dd.MM.yy HH:mm');

  return formatted;
}
