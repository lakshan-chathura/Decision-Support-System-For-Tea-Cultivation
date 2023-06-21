import React from 'react'
import axios from 'axios'
import './ProjectSetup.css'

export default function ProjectSetup(props){

  const BASE_URL = 'http://localhost:8000/api/'

  function updateStatusAndProgress(statusText,progressValue,overallProgressvalue){
    return new Promise((resolve,reject) => {
        try{
          let progress = document.getElementById('activity_progressbar')
          let mainProgress = document.getElementById('main_progressbar')
          let status = document.getElementById("lbl_status")

          status.innerHTML = "Status : " + statusText
          progress.innerHTML = progressValue + "%"
          progress.style.width = progressValue + "%"
          mainProgress.innerHTML = overallProgressvalue + "%"
          mainProgress.style.width = overallProgressvalue + "%"
          resolve(true)
        }
        catch(error){
          resolve(false)
        }
    })
  }

  function uploadFiles(filePickerID,project_real_name,mode){
    return new Promise((resolve,reject) => {
      let imageUploader = document.getElementById(filePickerID)

      let imagesData = new FormData()

      for(let i=0;i<imageUploader.files.length;i++){
        console.log(imageUploader.files[i]);
        imagesData.append('images[]',imageUploader.files[i],imageUploader.files[i].name)
      }

      axios.put(BASE_URL + 'images/upload/' + project_real_name + '/' + mode,
                 imagesData,
                 {
                   onUploadProgress: progressEvent => {
                     let progress = document.getElementById('activity_progressbar')
                     let value = Math.round((progressEvent.loaded / progressEvent.total) * 100)
                     progress.innerHTML = value + "%"
                     progress.style.width = value + "%"
                   }
                 }
               ).then((result) => {
        console.log(result)
        resolve(result)
      }).catch((error) => {
        reject(error)
      })
    })
  }

  function geotaggImages(project_absolute_name){
    return new Promise((resolve,reject) => {
        try{
          axios.post(BASE_URL + 'maps/geotag',{'project_name':project_absolute_name}).then((result) => {
            console.log(result)
            console.log("Images geotagged for " + project_absolute_name)
          }).then((result) => {
            updateStatusAndProgress('Geotagging images','100',Math.round((100/12) * 3))
            resolve(result)
          })
        }
        catch(error){
          console.log(error)
          reject(error)
        }
    })
  }

  function createOrthomosaic(project_absolute_name,mode){
    return new Promise((resolve,reject) => {
        try{
          let number = 0
          if(mode === 'rgb'){
            number = 4
          }
          else if(mode === 'nir'){
            number = 5
          }

          axios.post(BASE_URL + 'maps/mapping',{'project_name':project_absolute_name,'mode':mode})
          .then((result) => {
              console.log(result)
              return result
          }).then((result) => {
            console.log(result)
            updateStatusAndProgress('Creating " + mode + " orthomosaic','100',Math.round((100/12) * number))
            console.log(mode + " orthomosaic created for " + project_absolute_name);
            resolve(result)
          })
        }
        catch(error){
          console.log(error)
          reject(error)
        }
    })
  }

  function overlapOrthomosaics(project_absolute_name){
    return new Promise((resolve,reject) => {
      try{
        axios.post(BASE_URL + 'maps/align',{'project_name':project_absolute_name}).then((result) => {
          console.log(result)
        }).then((result) => {
          updateStatusAndProgress('Overlapping orthomosaics','100',Math.round((100/12) * 6))
          console.log("Orthomosaics overlapped in " + project_absolute_name);
          resolve(result)
        })
      }
      catch(error){
        console.log(error)
        reject(error)
      }
    })
  }

  function identifyTeadBuds(project_absolute_name){
    return new Promise((resolve,reject) => {
      try{
        axios.post(BASE_URL + 'maps/rgb/analyze/',{'project_name':project_absolute_name}).then((result) => {
          console.log(result)
        }).then((result) => {
          updateStatusAndProgress('Overlapping orthomosaics','100',Math.round((100/12) * 6))
          console.log("Identifying tea buds for " + project_absolute_name)
          resolve(result)
        })
      }
      catch(error){
        console.log(error)
        reject(error)
      }
    })
  }

  function createNDVIMapAndDoHealthAnalysis(project_absolute_name){
    return new Promise(function(resolve, reject) {
        try{
          axios.post(BASE_URL + 'maps/ndvi/',{'project_name':project_absolute_name}).then((result) => {
            console.log(result)
            updateStatusAndProgress('Creating the NDVI map','100',Math.round((100/12) * 8))
            console.log("Created NDVI map for " + project_absolute_name);
            resolve(result)
          })
        }
        catch(error){
          console.log(error)
          reject(error)
        }
    });
  }

  // function doHealthAnalysis(project_absolute_name){
  //   updateStatusAndProgress('Performing plant health analysis','100',Math.round((100/12) * 9))
  //   console.log("Doing health analysis for " + project_absolute_name);
  // }

  function createImageTiles(mode,project_absolute_name){
    return new Promise((resolve,reject) => {
        try{
          axios.put(BASE_URL + 'maps/tiles/create/',{'project_name':project_absolute_name,'mode':mode}).then((result) => {
            let number = 0
            if(mode === 'rgb'){
              number = 10
            }
            else if(mode === 'nir'){
              number = 11
            }
            else{
              number = 12
            }
            updateStatusAndProgress('Creating tiles for " + mode + " map','100',Math.round((100/12) * number))
            console.log("Created " + mode + " image tiles for " + project_absolute_name)
            console.log(result)
            resolve(result)
          })
        }
        catch(error){
          console.log(error)
          reject(error)
        }
    })
  }

  async function doSubmit(result){
    await updateStatusAndProgress('Uploading RGB Dataset','0',Math.round((100/12) * 1))
    await uploadFiles('rgbImageUploader',result.data.project_real_name,'rgb')

    await updateStatusAndProgress('Uploading NIR Dataset','0',Math.round((100/12) * 2))
    await uploadFiles('nirImageUploader',result.data.project_real_name,'nir')

    await updateStatusAndProgress('Geotagging images','0',Math.round((100/12) * 3))
    // await geotaggImages(result.data.project_real_name)
    await updateStatusAndProgress('Geotagging images','100',Math.round((100/12) * 3))

    await updateStatusAndProgress('Creating RGB orthomosaic','0',Math.round((100/12) * 4))
    await createOrthomosaic(result.data.project_real_name,'rgb')
    await updateStatusAndProgress('Creating RGB orthomosaic','100',Math.round((100/12) * 4))

    await updateStatusAndProgress('Creating NIR orthomosaic','0',Math.round((100/12) * 5))
    await createOrthomosaic(result.data.project_real_name,'nir')
    await updateStatusAndProgress('Creating NIR orthomosaic','100',Math.round((100/12) * 4))

    await updateStatusAndProgress('Overlapping orthomosaics','0',Math.round((100/12) * 6))
    await overlapOrthomosaics(result.data.project_real_name)
    await updateStatusAndProgress('Overlapping orthomosaics','100',Math.round((100/12) * 6))

    await updateStatusAndProgress('Analysing tea buds','0',Math.round((100/12) * 7))
    await identifyTeadBuds(result.data.project_real_name)

    await updateStatusAndProgress('Creating the NDVI map performing health analysis','0',Math.round((100/12) * 8))
    await createNDVIMapAndDoHealthAnalysis(result.data.project_real_name)
    await updateStatusAndProgress('Creating the NDVI map performing health analysis','100',Math.round((100/12) * 9))

    await updateStatusAndProgress('Creating tiles for RGB map','0',Math.round((100/12) * 10))
    await createImageTiles('rgb',result.data.project_real_name)
    await updateStatusAndProgress('Creating tiles for RGB map','100',Math.round((100/12) * 10))

    await updateStatusAndProgress('Creating tiles for NIR map','0',Math.round((100/12) * 11))
    await createImageTiles('nir',result.data.project_real_name)
    await updateStatusAndProgress('Creating tiles for NIR map','100',Math.round((100/12) * 11))

    await updateStatusAndProgress('Creating tiles for NDVI map','0',Math.round((100/12) * 12))
    await createImageTiles('ndvi',result.data.project_real_name)
    await updateStatusAndProgress('Process is completed','100',Math.round((100/12) * 12))

    await updateStatusAndProgress('Creating tiles for cluster map','0',Math.round((100/12) * 12))
    await createImageTiles('cluster',result.data.project_real_name)
    await updateStatusAndProgress('Process is completed','100',Math.round((100/12) * 12))
  }

  function submitForm(e){
    e.preventDefault()
    let transferObject = {
      'project_name':document.getElementById('txt_projectName').value
    }
    axios.post('http://localhost:8000/api/project/setup/',transferObject).then((result) =>{
        doSubmit(result)
    })
  }

  function onFileHandlerChanged(e){
      document.getElementById('lbl_' + e.target.id).innerHTML = e.target.files.length + " files selected"
  }

  return(
    <div className="setupBody col-md-6">
      <h1>Project Setup</h1>
      <hr/>
      <form encType="multipart/form-data" method="post" className="col-md-12" style={{padding:'0px'}}>
        <div className="input-group mb-3">
          <div className="input-group-prepend">
            <span className="input-group-text form-control-custom" id="basic-addon1">Project Name</span>
          </div>
          <input id="txt_projectName" type="text" className="form-control form-control-custom" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1"/>
        </div>
        <div className="input-group mb-3">
          <div className="input-group-prepend">
            <span className="input-group-text form-control-custom" id="basic-addon1">RGB Images&nbsp;&nbsp;&nbsp;</span>
          </div>
          <div className="custom-file">
            <input id="rgbImageUploader" multiple name="rgbImageUploader[] "type="file" className="custom-file-input" onChange={onFileHandlerChanged}/>
            <label id="lbl_rgbImageUploader" className="custom-file-label" htmlFor="rgbImageUploader">Choose file</label>
          </div>
        </div>
        <div className="input-group mb-3">
          <div className="input-group-prepend">
            <span className="input-group-text form-control-custom" id="basic-addon1">NIR Images&nbsp;&nbsp;&nbsp;&nbsp;</span>
          </div>
          <div className="custom-file">
            <input id="nirImageUploader" multiple name="nirImageUploader[]" type="file" className="custom-file-input" onChange={onFileHandlerChanged}/>
            <label id="lbl_nirImageUploader" className="custom-file-label" htmlFor="nirImageUploader">Choose file</label>
          </div>
        </div>
        <button className="btn btn-custom btn-primary" onClick={submitForm}>Submit</button>
      </form>
      <hr/>
      <p id="lbl_status" className="form-control-custom" style={{paddingTop:"10px"}}>Status</p>
      <div className="progress col-md-12 progressBar-custom">
        <div id="activity_progressbar" className="progress-bar" role="progressbar" style={{width: "0%"}} aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">0%</div>
      </div>
      <p style={{paddingTop:"10px"}} className="form-control-custom">Overall Progress</p>
      <div className="progress col-md-12 progressBar-custom">
        <div id="main_progressbar" className="progress-bar bg-success" role="progressbar" style={{width: "0%"}} aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">0%</div>
      </div>
    </div>
  )
}
