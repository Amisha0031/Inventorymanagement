import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Plus } from 'lucide-react';
import api from '../lib/api';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Badge } from '../components/ui/badge';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table';

const Products = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const { data: products, isLoading } = useQuery({
    queryKey: ['products'],
    queryFn: async () => {
      const res = await api.get('/products');
      return res.data;
    },
  });

  const filteredProducts = products?.filter(
    (p: any) =>
      p.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      p.sku?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Products</h1>

        <Button
          onClick={async () => {
            try {
              const response = await api.post('/products', {
                name: 'Test Product',
                sku: 'TEST' + Date.now(),
                description: 'Test Description',
                category: 'General',
                price: 100,
                quantity_in_stock: 10,
              });

              console.log(response.data);
              alert('Product Added Successfully');
              window.location.reload();
            } catch (error: any) {
              console.error(error);

              if (error.response) {
                alert(JSON.stringify(error.response.data));
              } else {
                alert(error.message);
              }
            }
          }}
        >
          <Plus className="mr-2 h-4 w-4" />
          Add Product
        </Button>
      </div>

      <div className="flex items-center space-x-2">
        <Input
          placeholder="Search products..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-sm"
        />
      </div>

      <div className="rounded-md border bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>SKU</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Price</TableHead>
              <TableHead>Stock</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center">
                  Loading...
                </TableCell>
              </TableRow>
            ) : filteredProducts?.length ? (
              filteredProducts.map((product: any) => (
                <TableRow key={product.id}>
                  <TableCell className="font-medium">
                    {product.name}
                  </TableCell>

                  <TableCell>{product.sku}</TableCell>

                  <TableCell>{product.category}</TableCell>

                  <TableCell>
                    ${Number(product.price).toFixed(2)}
                  </TableCell>

                  <TableCell>
                    {product.quantity_in_stock}
                  </TableCell>

                  <TableCell>
                    {product.quantity_in_stock > 10 ? (
                      <Badge variant="default">
                        In Stock
                      </Badge>
                    ) : product.quantity_in_stock > 0 ? (
                      <Badge variant="secondary">
                        Low Stock
                      </Badge>
                    ) : (
                      <Badge variant="destructive">
                        Out of Stock
                      </Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6} className="text-center">
                  No products found
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
};

export default Products;