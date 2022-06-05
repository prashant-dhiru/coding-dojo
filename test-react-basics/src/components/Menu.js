import './Menu.css';
import {Tab, Tabs} from "@mui/material";

function Menu() {
  return (
    <div className="Menu">
      <Tabs aria-label="basic tabs example" variant="fullWidth">
        <Tab label="Create Chain Task" />
        <Tab label="Show Task List" />
        <Tab label="Show Task" />
      </Tabs>
    </div>
  );
}

export default Menu;
