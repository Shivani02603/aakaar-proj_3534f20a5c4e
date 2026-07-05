import { useState, useEffect } from "react";
import { api } from "../api/client";
import { Todo } from "../types";

export default function Todos() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [newTodo, setNewTodo] = useState<Partial<Todo>>({
    title: "",
    description: "",
    due_date: "",
  });

  useEffect(() => {
    const fetchTodos = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get<Todo[]>("/api/todos");
        setTodos(response.data);
      } catch (err) {
        setError("Failed to load todos.");
      } finally {
        setLoading(false);
      }
    };
    fetchTodos();
  }, []);

  const handleCreateTodo = async () => {
    if (!newTodo.title) return;
    setLoading(true);
    setError(null);
    try {
      const response = await api.post<Todo>("/api/todos", newTodo);
      setTodos((prev) => [...prev, response.data]);
      setNewTodo({ title: "", description: "", due_date: "" });
    } catch (err) {
      setError("Failed to create todo.");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTodo = async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      await api.delete(`/api/todos/${id}`);
      setTodos((prev) => prev.filter((todo) => todo.id !== id));
    } catch (err) {
      setError("Failed to delete todo.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTodo = async (id: string, updatedTodo: Partial<Todo>) => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.put<Todo>(`/api/todos/${id}`, updatedTodo);
      setTodos((prev) =>
        prev.map((todo) => (todo.id === id ? response.data : todo))
      );
    } catch (err) {
      setError("Failed to update todo.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Todos</h1>
      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Title"
          value={newTodo.title}
          onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
          className="border p-2 rounded w-full mb-2"
        />
        <textarea
          placeholder="Description"
          value={newTodo.description || ""}
          onChange={(e) =>
            setNewTodo({ ...newTodo, description: e.target.value })
          }
          className="border p-2 rounded w-full mb-2"
        />
        <input
          type="datetime-local"
          value={newTodo.due_date || ""}
          onChange={(e) => setNewTodo({ ...newTodo, due_date: e.target.value })}
          className="border p-2 rounded w-full mb-2"
        />
        <button
          onClick={handleCreateTodo}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Create Todo
        </button>
      </div>
      <ul>
        {todos.map((todo) => (
          <li
            key={todo.id}
            className="border p-4 rounded mb-2 flex justify-between items-center"
          >
            <div>
              <h2 className="font-bold">{todo.title}</h2>
              <p>{todo.description}</p>
              <p className="text-sm text-gray-500">
                Due: {todo.due_date ? new Date(todo.due_date).toLocaleString() : "None"}
              </p>
              <p className="text-sm text-gray-500">
                Completed: {todo.completed ? "Yes" : "No"}
              </p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() =>
                  handleUpdateTodo(todo.id, { completed: !todo.completed })
                }
                className="bg-green-500 text-white px-4 py-2 rounded"
              >
                {todo.completed ? "Mark Incomplete" : "Mark Complete"}
              </button>
              <button
                onClick={() => handleDeleteTodo(todo.id)}
                className="bg-red-500 text-white px-4 py-2 rounded"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
      {todos.length === 0 && !loading && (
        <p className="text-gray-500">No todos found.</p>
      )}
    </div>
  );
}