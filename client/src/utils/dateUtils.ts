export const truncateToMinutes = (date: string): number => {
  const d = new Date(date);
  d.setSeconds(0);
  d.setMilliseconds(0);
  return d.getTime();
};

export const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const isEqualCreateAndUpdateDates = (
  createdAt: string,
  updatedAt: string,
) => {
  return truncateToMinutes(createdAt) === truncateToMinutes(updatedAt);
};
