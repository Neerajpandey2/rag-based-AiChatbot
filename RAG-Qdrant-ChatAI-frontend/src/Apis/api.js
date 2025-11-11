import { toast } from "react-toastify";
// api.js
const API_URL = "http://localhost:5000";  // Flask backend

// ---- Collections ----
export const createCollection = (name) => {
  return fetch(`${API_URL}/create_collection`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  }).then((res) => res.json());
};

export const deleteCollection = (name) => {
  return fetch(`${API_URL}/delete_collection?name=${name}`, {
    method: "DELETE",
  }).then((res) => res.json());
};

// ---- Q&A Insert ----
export const insertQA = (collection, question, answers, vector = []) => {
  const params = new URLSearchParams({
    name: collection,
    "Payload.Question": question,
    "Payload.Answers": answers,
  });
  vector.forEach((v) => params.append("Vector", v));

  return fetch(`${API_URL}/insert_Q&A?${params.toString()}`, {
    method: "POST",
  }).then((res) => res.json());
};

export const bulkInsertQA = (collection, qaList) => {
  return fetch(`${API_URL}/bulk_qa_insert?collection=${collection}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(qaList),
  }).then((res) => res.json());
};

// ---- Get Q&A with pagination ----
export const getQAPaginated = async (collection = "CustomAi", limit = 25, offset = null) => {
  try {
    let url = `${API_URL}/qdrantapi/getQAsPaginated?collection=${collection}&limit=${limit}`;
    if (offset) {
      url += `&offset=${offset}`;
    }

    const res = await fetch(url, { method: "GET" });

    if (!res.ok) {
      throw new Error("Failed to fetch questions and answers");
    }

    return await res.json(); // will include { total_points, fetched, next_page_offset, qa_list }
  } catch (err) {
    console.error("Error fetching paginated Q&A:", err);
    return { error: err.message };
  }
};




export const deleteQuestionById = (collection, questionId) => {
  return fetch(
    `${API_URL}/deleteQuestionById?collection_name=${collection}&questionId=${questionId}`,
    { method: "DELETE" }
  ).then((res) => res.json());
};

// ---- Search ----
export const searchQA = async (collection, query) => {
  try {
    const response = await fetch(`${API_URL}/qdrantapi/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ collection, query }),
    });

    const result = await response.json(); // store in variable
    console.log("Search result:", result); // debug log

    return result; // return the variable
  } catch (err) {
    console.error("Search API failed:", err);
    return { error: err.message };
  }
};

// ---- PDF Upload ----
export const uploadPdf = async (file, collection_name = "CustomAi") => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("collection_name", collection_name);

  try {
    const res = await fetch(`${API_URL}/upload/`, {
      method: "POST",
      body: formData,
    });
    return await res.json();
  } catch (err) {
    console.error("Upload PDF failed:", err);
    return { error: err.message };
  }
};

//store qa pairs into db
export const saveQaPairs = async (collectionName , data) => {
  try {
    const res = await fetch(
      `${API_URL}/qdrantapi/bulk_qa_insert?collection=${collectionName}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data), // send array directly
      }
    );
    if (res.ok) {
       toast.success("successfully saved to db");
    }
    else{
       toast.error("save to db failed");
    }

    return await res.json();
  } catch (error) {
    console.error("Error saving QA pairs:", error);
    return { error: error.message };
  }
};

// add a single Q&A point
export const addQAPoint = async (collection, question, answer) => {
  try {
    const res = await fetch(`${API_URL}/qdrantapi/insert_Q&A?collection_name=${collection}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, answer }), // body JSON
    });

    if (res.ok) {
      toast.success("Q&A added successfully");
    } else {
      toast.error("Failed to add Q&A");
    }

    return await res.json();
  } catch (err) {
    console.error("Error adding Q&A:", err);
    toast.error("Something went wrong while adding");
    return { error: err.message };
  }
};



// edit/update a Q&A point by id
export const editQAPoint = async (collection, id, question, answer) => {
  try {
    const res = await fetch(`${API_URL}/qdrantapi/update_QA?collection_name=${collection}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, question, answer }),
    });

    if (res.ok) {
      toast.success("Q&A updated successfully");
    } else {
      toast.error("Failed to update Q&A");
    }

    return await res.json();
  } catch (err) {
    console.error("Error updating Q&A:", err);
    toast.error("Something went wrong while updating");
    return { error: err.message };
  }
};


//delete a Q&A point by id
export const deleteQAPoint = async (collection, id) => {
  try {
    const res = await fetch(
      `${API_URL}/qdrantapi/deleteQuestionById?collection_name=${collection}&questionId=${id}`,
      { method: "DELETE" }
    );

    if (res.ok) {
      toast.success("Q&A deleted successfully");
    } else {
      toast.error("Failed to delete Q&A");
    }

    return await res.json();
  } catch (err) {
    console.error("Error deleting Q&A:", err);
    toast.error("Something went wrong while deleting");
    return { error: err.message };
  }
};
