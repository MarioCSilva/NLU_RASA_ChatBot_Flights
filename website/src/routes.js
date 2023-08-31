import HomePage from './pages/home_page.js';
const { Outlet } = require("react-router-dom");

const routes = () => [
    {
        path: "/",
        element: <Outlet />,
        children: [
            { path: "/home", element: <HomePage/> },
        ]
    },
]

export default routes;