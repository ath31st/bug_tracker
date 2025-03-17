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

export const getPriorityIcon = (priority: string): string => {
  switch (priority) {
    case 'CRITICAL':
      return 'mdi-alert-circle';
    case 'HIGH':
      return 'mdi-arrow-up';
    case 'MEDIUM':
      return 'mdi-minus';
    case 'LOW':
      return 'mdi-arrow-down';
    default:
      return 'mdi-help';
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

export const priorityOrder = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
