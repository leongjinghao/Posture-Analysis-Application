using Microsoft.EntityFrameworkCore;
using PostureLogApi.Models;

namespace PostureLogApi.Data
{
    public class DataContext: DbContext, IDataContext
    {
        public DataContext(DbContextOptions<DataContext> options) : base(options)
        {
             
        }
 
        public DbSet<PostureLog> PostureLogs { get; init; }
    }
}