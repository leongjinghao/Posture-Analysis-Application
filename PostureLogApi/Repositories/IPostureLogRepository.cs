using System.Collections.Generic;
using System.Threading.Tasks;
using PostureLogApi.Models;

namespace PostureLogApi.Repositories
{
    public interface IPostureLogRepository
    {
        Task<PostureLog> Get(int id);
        Task<IEnumerable<PostureLog>> GetAll();
        Task Add(PostureLog postureLog);
        Task Delete(int id);
        Task Update(PostureLog postureLog);
    }
}