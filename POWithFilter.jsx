import React, { useEffect, useRef, useState } from 'react';
import ProjectOverviewSingleProject from './ProjectOverviewSingleProject';
import LoadingIcon from '../images/Loading_icon.gif';

export default function POWithFilter(props) {
  const {
    searchInput,
    zohoIdFilter,
    statusFilter,
    ownerFilter,
    filterPage,
    users,
    setFilterPage,
  } = props;

  const [projects, setProjects] = useState([]);
  const bottomRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hasMoreProjects, setHasMoreProjects] = useState(true);

  // Fetch projects from the API when the filter criteria change
  useEffect(() => {
    setProjects([]);
    setFilterPage(1);
    setHasMoreProjects(true);
  }, [searchInput, zohoIdFilter, statusFilter, ownerFilter]);

  useEffect(() => {
    // Load more projects when the user scrolls to the bottom of the page
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !isLoading && hasMoreProjects) {
        setIsLoading(true);
        setFilterPage((prevPage) => prevPage + 1);
      }
    });

    if (bottomRef.current) {
      observer.observe(bottomRef.current);
    }

    return () => {
      if (bottomRef.current) {
        observer.unobserve(bottomRef.current);
      }
    };
  }, [isLoading, hasMoreProjects, setFilterPage]);

  useEffect(() => {
    // Fetch projects from the API based on the filter criteria and pagination
    const fetchProjects = async () => {
      setIsLoading(true);

      try {
        const url = 'http://localhost:5000/api/filter-projects';
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            searchInput,
            zohoIdFilter,
            statusFilter,
            ownerFilter,
            filterPage,
          }),
        });

        const data = await response.json();

        if (data.data.length > 0) {
          if (data.data.length < 100) {
            setHasMoreProjects(false);
          }

          if (filterPage === 1) {
            setProjects(data.data);
          } else {
            setProjects((prevProjects) => [...prevProjects, ...data.data]);
          }
        } else {
          setHasMoreProjects(false);
        }
      } catch (error) {
        console.error(error);
      }

      setIsLoading(false);
    };

    fetchProjects();
  }, [searchInput, zohoIdFilter, statusFilter, ownerFilter, filterPage]);

  return (
    <div>
      {projects.map((project, index) => (
        <ProjectOverviewSingleProject
          key={index}
          project={project}
          users={users}
          filtering={true}
        />
      ))}

      {isLoading && (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
          <img src={LoadingIcon} style={{ height: '60px' }} alt="Loading projects..." />
        </div>
      )}

      {!isLoading && hasMoreProjects && projects.length > 0 && (
        <div ref={bottomRef} style={{ textAlign: 'center', marginTop: '50px' }}>
            <img src={LoadingIcon} style={{ height: '60px' }} alt="Loading projects..." />
        </div>
        )}
    
        {!isLoading && !hasMoreProjects && projects.length === 0 && (
            <div style={{ textAlign: 'center', marginTop: '50px' }}>
                <p>No projects found</p>
            </div>
        )}
    </div>
    );
}