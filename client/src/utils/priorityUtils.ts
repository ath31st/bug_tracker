export const getPriorityName = (priority: string) => {
  switch (priority) {
    case 'LOW':
      return 'Низкий';
    case 'MEDIUM':
      return 'Средний';
    case 'HIGH':
      return 'Высокий';
    case 'CRITICAL':
      return 'Критический';
    default:
      return 'Неизвестно';
  }
};

export const getPriorityColor = (priority: string) => {
  switch (priority) {
    case 'LOW':
      return 'green';
    case 'MEDIUM':
      return 'yellow';
    case 'HIGH':
      return 'orange';
    case 'CRITICAL':
      return 'red';
    default:
      return 'grey';
  }
};
