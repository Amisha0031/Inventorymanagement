import { Bell } from 'lucide-react';

const Navbar = () => {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-card px-6">
      <div className="flex-1" />
      <div className="flex items-center gap-4">
        <button className="rounded-full p-2 text-muted-foreground hover:bg-muted">
          <Bell className="h-5 w-5" />
        </button>
        <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
          AD
        </div>
      </div>
    </header>
  );
};
export default Navbar;
