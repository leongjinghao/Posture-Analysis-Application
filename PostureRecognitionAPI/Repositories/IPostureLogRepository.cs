using System.Collections.Generic;
using System.Threading.Tasks;
using PostureRecognitionAPI.Models;

namespace PostureRecognitionAPI.Repositories
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