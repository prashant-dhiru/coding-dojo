import './Menu.css';
import React from "react";

export const taskNodeContext = React.createContext("hello");

function TaskNode() {
  const value = React.useContext(taskNodeContext);
  return (
    <>
      {value}
    </>
  )
}

function CreateChainTask() {
  // const [nodeDate, setNodeData] = useState("hello")
  return (
    <taskNodeContext.Provider value="string">
      <TaskNode>"data"</TaskNode>
    </taskNodeContext.Provider>
  );
}


export default CreateChainTask;
