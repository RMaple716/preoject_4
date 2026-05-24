import Home from '../pages/Home';
import RequirementForm from '../pages/RequirementFormNew';
import ItineraryList from '../pages/ItineraryList';
import ItineraryDetail from '../pages/ItineraryDetail';
import TaskStatus from '../pages/TaskStatusNew';

export const routes = [
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/requirement',
    element: <RequirementForm />,
  },
  {
    path: '/itineraries',
    element: <ItineraryList />,
  },
  {
    path: '/itinerary/:id',
    element: <ItineraryDetail />,
  },
  {
    path: '/task/:taskId',
    element: <TaskStatus />,
  },
];
