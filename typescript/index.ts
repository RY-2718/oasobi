type Product = {
  name: string;
  category: string;
  price: number;
};

function groupProductsByCategory(
  products: Product[]
): Record<string, Product[]> {
  return products.reduce(
    (groups, product) => {
      let group = groups[product.category];
      if (!group) {
        group = [];
        groups[product.category] = group;
      }
      group.push(product);
      return groups;
    },
    {} as Record<string, Product[]>
  );
}

function main(): void {
  const products: Product[] = [
    { name: "Apple", category: "fruit", price: 100 },
    { name: "Banana", category: "fruit", price: 150 },
    { name: "Carrot", category: "vegetable", price: 200 },
  ];

  const grouped = groupProductsByCategory(products);

  console.log(grouped);
}

main();
