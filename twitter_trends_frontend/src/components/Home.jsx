import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useEffect } from 'react'
import axios from 'axios'
function Home() {
    const navigate = useNavigate()

    const [trends,setTrends] = useState([])
    const [ipAddress,setIpAddress] = useState(null);
    const [loading,setLoading] = useState(false);
    const [objectID,setObjectID] = useState(null);
    const [date,setDate] = useState(null);
    const [mongoData,setMongoData] = useState(null);
    const handleFetchTrends = async () =>{
        console.log("CALLING HANDLE FETCH TRENDS");
        setLoading(true)
        try {
            const response = await axios.get("http://127.0.0.1:4000/fetch_trends")
            console.log("response",response)
            if(response.error){
                console.log("Could not fetch current Trends")
                return ;
            }
            console.log("PRINTING RESPONSE",response)
            setTrends(response.data.trends);
            setIpAddress(response.data.ip_address)
            setDate(response.data.timestamp)
            setObjectID(response.data.object_id)
            setMongoData(response.data.mongoData)
        } catch (error) {
            console.log("Could not fetch Trends",error);
        }
        
        setLoading(false);
    }
    
    return (
    <div className='mx-auto w-11/12 max-w-maxContent place-content-center pt-5'>

        {
            trends.length > 0 ? (
                <div>
                    These are the most happening topics as on {date}
                        <div className='flex flex-col gap-2'>
                        {
                            trends.map((trend,index) =>{
                                return(
                                    <div className='flex flex-col gap-2' key={index}>
                                    {trend}
                                    </div>  
                                )
                            })
                        }
                        </div>
                        
                    <div>
                        <p>The IP address used for this query was {ipAddress}</p>
                    </div>
                    <div>
                        <p>Here’s a JSON extract of this record from the MongoDB:</p>
                        <div>
                            {
                                mongoData && (
                                    <div>
                                        <h3>Trends</h3>


                                        <p><strong>Object ID:</strong> {objectID}</p>

    
                                        <p><strong>IP Address:</strong> {ipAddress}</p>

                                        <p><strong>Timestamp:</strong> {date}</p>

                                        <h4>Trends:</h4>
                                        <ul>
                                            {trends.map((trend, index) => (
                                                <li key={index}>{trend}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )
                            }
                        </div>
                    </div>
                    <button 
                    onClick={handleFetchTrends}
                    className='text-blue-300 underline'>Click here to run the query again.
                    </button>
                </div>
            ) :
            (
                
                <div className='space-y-5'>
                    <button 
                    onClick={handleFetchTrends}
                    className='text-blue-300 underline '>Click here to run the script.
                    </button>
                    <p>No Trends Fetched Yet</p>
                </div>
            )
        }
    </div>
  )
}

export default Home