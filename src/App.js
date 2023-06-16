import React, { useState, useEffect, useCallback, useMemo} from 'react';
import './App.css'
import axios from 'axios';



function App(){
  
  const [inputs, setInputs] = useState([]);
  const server_down_msg = useMemo(() =>{
    return {"message": "The Server is Down... Try Later"}}, []);

  const [msg, setMsg] = useState(server_down_msg);
  const [supportedWebsites, setSupportedWebsites] = useState([]);
  const server_url = "https://flask-scraper.vercel.app//";
  const [waiting, setWaiting] = useState(false);

  const addInput = () => {
    setInputs([...inputs, {label: "הכנס קישור", value: ""}]);};

  /**collect the inputs to a list*/
  const getWebsToScrap = () => {
    let webs_to_scrap = [];
    for(let j=0; j<inputs.length;j++){
      let web = inputs[j].value
      if(inputs[j].label === "לא נתמך")
        continue
      if(web.length>2)
        webs_to_scrap.push(web)
    }
    return webs_to_scrap
  };

  const checkIfWebsToScrap = (webs_to_scrap) => {
    if(webs_to_scrap.length === 0){
      window.alert("אין אתרים נתמכים ליצירת קובץ אקסל, נסו להוסיף אתרים נתמכים")
      setWaiting(false)
      return false;
    }
    return true;
  };

  const getFilename = () => {
    let filename = "file";
    try{
      const currenttime = new Date();
      filename = "MusicalInstrumentsScraper" + " " + currenttime.toLocaleString();
    } 
    catch(e){
      console.log(e);
    }
    return filename + ".xlsx"
  };


  const askServerForDownload = () => {
    console.log("asking server for a download")
    return axios({
      headers: {'Cache-Control': 'no-cache'},
      url: server_url + 'download',
      method: 'GET',
      responseType: 'blob',
    }).then((response) => {
      console.log('response from server:', response);
      return response; // return the response object
    })
    .catch((error) => {
      console.log('error from server:', error);
      throw error; // re-throw the error so it can be caught by the caller
    });
  };

  const serveTheDownload = (response) => {
    console.log("server the download");
    console.log(response.data)
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    const filename = getFilename();
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
  };



  const askServerToScrap = (webs_to_scrap) => {
    console.log("asking server to scrap");
    setWaiting(true);
    axios.post(server_url + 'scrap', { webs_to_scrap })
    .then((response) => {
      console.log("server finished scraping");
      console.log("asking server for a download");
        return askServerForDownload();}) //return response
      .catch((e)=>{
        console.log(e);
        setWaiting(false);})
      .then((response) => {        
        console.log(response.data)
        if(!(response.statusText === "OK")){
          console.log("failed");
          window.alert(response.message);
          console.log(response.data);
          setWaiting(false);
          return;
        }
        console.log("returned from server with waiting = " + waiting)
        serveTheDownload(response); //opens a download dialog
        console.log("finished with waiting = " + waiting)
        setWaiting(false);
      })
  }
  
  /**runs every 10 seconds to check if the server is up */
  const checkServer = useCallback(async () => {
    fetch(server_url)
    .then(response => {
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      return response.json();
    })
    .then(msg => setMsg(msg))
    .catch(error => {
      console.error(error);
      setMsg(server_down_msg);
      setWaiting(false)
      });
  },[server_down_msg, server_url, setMsg, setWaiting]);

  useEffect(() => {
    checkServer();
    const intervalId = setInterval(checkServer, 10000);
    return () => clearInterval(intervalId);
  }, [checkServer]);

  useEffect(() => {
    fetch(server_url + "websites")
      .then(response => {
        if(!response.ok){
          throw new Error(response.statusText);
        }
        return response.json();
      })
      .then(supportedWebsites => setSupportedWebsites(supportedWebsites))
      .catch((error) =>{ 
        console.error(error);
        setWaiting(false);
        });
  }, [setWaiting, waiting]);

  useEffect(()=>{
    console.log("waiting = " + waiting);
  },[waiting]);
  

  const getLabel = (url) => {
    if(url==="")
      return "הכנס קישור";
    for(let i=0; i<supportedWebsites.length; i++){
      if(url.indexOf(supportedWebsites[i][0])!==-1)
        return supportedWebsites[i][1];
    }
    return "לא נתמך";
  }
  
  const handleDelete = (index) => {
    console.log("called");
    console.log(index);
    setInputs(inputs.filter((elem, i)=>i!==index));
  }

  const handleSubmit = async (e) => {
    setWaiting(true);
    console.log("waiting = " + waiting);
    //get only non-empty input fields (values)
    let webs_to_scrap = getWebsToScrap();
    if(!checkIfWebsToScrap(webs_to_scrap)){
      console.log("no webs to scrap");
      setWaiting(false);
      return;
    }
    //request the server to create and send back the excel file
    try{
      console.log(webs_to_scrap);
      askServerToScrap(webs_to_scrap);
     }
    catch(error){
      console.log(error);
      setMsg("an error occured, try again");
    }
  }

  

  return(
    <div className="App">
      <h1>{msg && msg.message}</h1>
      <button id = "add-btn" disabled={waiting} onClick={addInput}>הוספת אתר</button>
      {inputs.map((input, index)=>(
      <div id= "field" key={index}>
        <button id = "del-btn" disabled={waiting} onClick={() => handleDelete(index)}>מחק</button>
        <input className="input" value={input.value} onChange={(e)=> {
          const newInputs = [...inputs];
          newInputs[index].value = e.target.value;
          newInputs[index].label = getLabel(e.target.value);
          setInputs(newInputs);
        }}/>
        <label className="label">{input.label}</label>
      </div>
    ))}
    <button id = "submit-btn" onClick={handleSubmit} disabled={waiting}> {`${waiting ? "עובדים על זה.." : "Scrap"}`}</button>
    </div>
  );
}



export default App;







