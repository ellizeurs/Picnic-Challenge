import React, { useEffect, useState } from "react";
import { api } from "../api";

interface CategoryCount {
  category: string;
  count: number;
}

export const CategoriesList: React.FC = () => {
  const [categories, setCategories] = useState<CategoryCount[]>([]);

  useEffect(() => {
    api.get<CategoryCount[]>("/categories")
      .then(res => setCategories(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h2>Category Counts</h2>
      <ul>
        {categories.map(cat => (
          <li key={cat.category}>
            {cat.category}: {cat.count}
          </li>
        ))}
      </ul>
    </div>
  );
};
