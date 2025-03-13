export const getStatusColor = (status: string) => {
  switch (status) {
    case 'NEW':
      return 'blue';
    case 'IN_PROGRESS':
      return 'orange';
    case 'RESOLVED':
      return 'green';
    case 'CLOSED':
      return 'grey';
    default:
      return 'grey';
  }
};

export const getStatusName = (status: string) => {
  switch (status) {
    case 'NEW':
      return 'Новый';
    case 'IN_PROGRESS':
      return 'В работе';
    case 'RESOLVED':
      return 'Решен';
    case 'CLOSED':
      return 'Закрыт';
    default:
      return 'Неизвестно';
  }
};
