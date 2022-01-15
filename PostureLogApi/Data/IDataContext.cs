using System.Threading;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using PostureLogApi.Models;

namespace PostureLogApi.Data
{
    public interface IDataContext
    {
        DbSet<PostureLog> PostureLogs { get; init; }
        Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
    }
}